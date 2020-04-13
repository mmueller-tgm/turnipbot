from turnipbot.offer import Offer


class SubmissionServerInterface:
    def serve_submission(self, offer: Offer) -> None:
        pass
