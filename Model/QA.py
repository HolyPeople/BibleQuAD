
class QA:
    def __init__(self, uuid, paragraph_id, question, answers, user_id, is_impossible=0, created_at=None):
        self.paragraph_id = paragraph_id
        self.question = question
        self.answers = answers
        self.uuid = uuid
        self.user_id = user_id
        self.created_at = created_at
        self.is_impossible = is_impossible
