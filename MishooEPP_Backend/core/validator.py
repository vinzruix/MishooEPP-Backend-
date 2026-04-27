from abc import ABC, abstractmethod


class ValidatorStrategy(ABC):
    @abstractmethod
    def validate(self,**kwargs):
        pass


class Validator:
    def __init__(self, validator_strategy : ValidatorStrategy):
        self._strategy = validator_strategy

    def set_validator(self, validator_strategy : ValidatorStrategy):
        self._strategy = validator_strategy


    def validate(self,**kwargs):
        return self._strategy.validate(**kwargs)