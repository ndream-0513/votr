from models import db, Users, Polls, Topics, Options, UserPolls
from flask import Blueprint, request, jsonify, session
from datetime import datetime


api = Blueprint('api', 'api', url_prefix='/api')

@api.route('/polls', methods=['GET', 'POST'])
# retrieves/adds polls from/to the database
def api_polls():
    if request.method == 'POST':
        # get the poll and save it in the database
        poll = request.get_json()
        print(poll)

        # simple validation to check if all values are properly secret
        for key, value in poll.items():
            if not value:
                return jsonify({'error': 'value for {} is empty'.format(key)})

        title = poll['title']
        options_query = lambda option : Options.query.filter(Options.name.like(option))

        options = [Polls(option=Options(name=option))
                    if options_query(option).count() == 0
                    else Polls(option=options_query(option).first()) for option in poll['options']
                    ]
        # 使用eta参数指定时间
        eta = datetime.utcfromtimestamp(poll['close_date'])

        new_topic = Topics(title=title, options=options, close_date=eta)

        db.session.add(new_topic)
        db.session.commit()

        from tasks import close_poll

        # 通过调用apply_async方法将任务发送给Celery
        close_poll.apply_async((new_topic.id,), eta=eta)

        return jsonify({'message': 'Poll was created succesfully'})

    else:
        # it's a GET request, return dict representations of the API
        polls = Topics.query.filter_by(status=1).join(Polls).order_by(Topics.id.desc()).all()
        all_polls = {'Polls':  [poll.to_json() for poll in polls]}

        return jsonify(all_polls)

@api.route('/polls/options')
def api_polls_options():

    all_options = [option.to_json() for option in Options.query.all()]

    return jsonify(all_options)

@api.route('/poll/vote', methods=['PATCH'])
def api_poll_vote():

    poll = request.get_json()

    poll_title, option = (poll['poll_title'], poll['option'])

    join_tables = Polls.query.join(Topics).join(Options)

    # Get topic and username from the database
    topic = Topics.query.filter_by(title=poll_title).first()
    user = Users.query.filter_by(username=session['user']).first()

    # filter options
    option = join_tables.filter(Topics.title.like(poll_title)).filter(Options.name.like(option)).first()

    # check if the user has voted on this poll     
    poll_count = UserPolls.query.filter_by(topic_id=topic.id).filter_by(user_id=user.id).count()
    if poll_count > 0:
        return jsonify({'message': 'Sorry! multiple votes are not allowed'})

    if option:
        # record user and poll
        user_poll = UserPolls(topic_id=topic.id, user_id=user.id)
        db.session.add(user_poll)

        # increment vote_count by 1 if the option was found
        option.vote_count += 1
        db.session.commit()

        return jsonify({'message': 'Thank you for voting'})

    return jsonify({'message': 'option or poll was not found please try again'})

@api.route('/poll/<poll_name>')
def api_poll(poll_name):
    poll = Topics.query.filter(Topics.title.like(poll_name)).first()

    return jsonify({'Polls': [poll.to_json()]}) if poll else jsonify({'message': 'poll not found'})
