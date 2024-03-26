def init_test(**kwargs):
    """Initiliazes running tests.

    Args:
        app (_type_): Currently running flask application.
    """
    from .generate_feedback import generate_tag, generate_comment, generate_comment_replies, generate_blogs, generate_users
    from .generate_quotes import quotes, feedback
    #generate_comment_replies(50, generate_comment(20))
    # generate_blogs(100, generate_comment(10), generate_tag(10))
    # generate_users(10)
    # quotes(50)
    # feedback(20)
