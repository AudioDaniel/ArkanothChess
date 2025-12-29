class UserInteraction: 
    """
    Handles interaction with the user via the command line.
    """

    @staticmethod
    def select_square(prompt_messsage : str) -> tuple[int,int]:
        """
        Prompts the user to select a square.
        :param prompt_messsage: The message to display to the user.
        :return: A tuple (x, y) representing the selected coordinates.
        """
        user_input : str = UserInteraction.sanitice_input(input(prompt_messsage))
        return UserInteraction.translate_input(user_input)

    @staticmethod
    def sanitice_input( user_input: str) -> str:
        """
        Sanitizes the user input by trimming whitespace and converting to lowercase.
        :param user_input: The raw user input.
        :return: The sanitized input string.
        """
        user_input = user_input.strip()
        user_input = user_input.lower()
        return user_input
    
    @staticmethod
    def translate_input( user_input: str) -> tuple[int,int]:
        """
        Translates algebraic notation (e.g., 'A1') to grid coordinates.
        :param user_input: The sanitized user input.
        :return: A tuple (x, y) representing the coordinates.
        """
        # Translate the input to a tuple of integers
        column, row = user_input[0].upper(), user_input[1]
        return (ord(column) - ord('A'), int(row) - 1)