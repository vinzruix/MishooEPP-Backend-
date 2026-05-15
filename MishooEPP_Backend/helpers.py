from MishooEPP_Backend.exeptions import ParameterEmpty


class RequestValidatorHelper:

    @staticmethod
    def search_empty_parameters(dictionary, excluded_keys: list = ()):


        for key, value in dictionary.items():
            if key in excluded_keys:
                continue

            if not value:
                raise ParameterEmpty(f"Parametro: {key} vacio")
