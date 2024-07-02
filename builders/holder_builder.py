from models.HolderModel import HolderModel


class HolderBuilder:

    @staticmethod
    def holder_builder(body):
        return HolderModel(name=body['name'], document=body['document'])
