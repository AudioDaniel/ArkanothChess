class UserInteraction: 

    @staticmethod
    def select_square(prompt_messsage : str) -> tuple[int,int]:
        user_input : str = UserInteraction.sanitice_input(input(prompt_messsage))
        return UserInteraction.translate_input(user_input)

    @staticmethod
    def sanitice_input( user_input: str) -> str:
        user_input = user_input.strip()
        user_input = user_input.lower()
        return user_input
    
    @staticmethod
    def translate_input( user_input: str) -> tuple[int,int]:
        # Translate the input to a tuple of integers
        column, row = user_input[0].upper(), user_input[1]
        return (ord(column) - ord('A'), int(row) - 1)