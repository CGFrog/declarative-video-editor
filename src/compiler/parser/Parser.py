from lexer.Lexer import Lexer
from lexer.Token import Token
from lexer.Token import TokenLabel as TL

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer : Lexer = lexer
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.timeline : dict = {} # Tells the compiler how to organize our video.
        self.line_number : int = 1

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        for line in lines_of_code:
            tokens = self.lexer.build_tokens(line)
            if len(tokens) == 0:
                continue
            
            token = tokens[0].key
            # There are only four things a line might do, create media, signal start of the timeline, add media to timeline, or signal render.
            match token:
                case TL.END_OF_LINE:
                    # White space, just ignore.
                    break
                case TL.MEDIA:
                    if tokens[1].key != TL.IDENTIFIER: 
                        raise Exception(f"Invalid identifier after type declaration.")
                    self.state[tokens[1].value] =  self.__parse_media(tokens)
                    break
                case TL.TIMELINE:
                    # Timeline is semantic sugar at this point, we may be able to just get rid of it.
                    break
                
                case TL.IDENTIFIER:
                    self.timeline[tokens[1].value] = self.__parse_timeline_instance(tokens)
                    break

                case TL.RENDER:
                    self.__parse_render()
                    # signal to compiler we are ready to compile the video.
                    break
            
            self.line_number += 1

    def __parse_render(self, tokens: list[Token]):
        index : int = 0
        while tokens[index] != TL.END_OF_LINE:
            match tokens[index].key:
                case TL.LBRACK:
                    # Determines final output render resolution, maybe some other stuff later idk I just work here.
                    end_bracket: int = self.__get_nest_termination_index(tokens, index, TL.RBRACK)
                    return self.__parse_resolution(tokens[index:end_bracket-1:])
                case _:
                    raise Exception(f"Unexpected argument: {tokens[index].value} on line {self.line_number}")


    def __parse_media(self, tokens : list[Token]):
        """
        When the parser detects a line dedicated to instantiating a media object, parse media determines:
        <ul>
            <li> Unions </li>
            <li> Trims </li>
            <li> Effects </li>
        </ul> 
        onto the specific media object.        
        """
        index : int = 0
        current_operator : TL | None = None
        while tokens[index].key != TL.END_OF_LINE:
            match tokens[index].key:
                case TL.UNION:
                    current_operator = TL.UNION
                    break
                case TL.DEFINITION:
                    current_operator = TL.DEFINITION
                    break
                case TL.LPAREN:
                    end_parenthesis: int = self.__get_nest_termination_index(tokens, index, TL.RPAREN)
                    # gets the time or function input
                    self.__parse_parenthesis(tokens[index+1:end_parenthesis-1:],current_operator)
                    index = end_parenthesis + 1
                    break
                case TL.FUNC_COMP:
                    current_operator = TL.FUNC_COMP
                    break
                case _:
                    raise Exception(f"Invalid syntax on line {self.line_number}")


    def __parse_timeline_instance(self, tokens : list[Token]):
        pass

    def __get_nest_termination_index(self, tokens: list[Token], current_index, termination_symbol: TL)-> int:
        """
        Helper function that determines the final index of the internals of parenthesis of brackets.        
        """
        for t in range(current_index+1, len(tokens)):
            if tokens[t].key == termination_symbol:
                return t
        raise Exception("Missing right parenthesis")

def __parse_parenthesis(self, tokens : list[Token], current_operator : TL | None):
        """
        Helper function that returns the clean values of the parenthesis internals:
        <ul>
            <li> Time duration </li>
            <li> Effect parameter </li>
        </ul>        
        """
        match current_operator:
            case None:
                raise Exception(f"No valid operator found after parenthesis.")
            case TL.UNION:
                return self.__construct_time(tokens)
            case TL.DEFINITION:
                return self.__construct_time(tokens)
            case TL.FUNC_COMP:    
                return self.__construct_function_input(tokens)
            
    def __construct_time(self, tokens : list[Token]):
        return "".join([t.value for t in tokens])

    def __construct_function_input(self, tokens : list[Token]):
        pass

    def __parse_resolution(self, tokens : list[Token]):
        # Inside of the brackets, we may have things such as resolution,
        for token in tokens:
            if token == TL.RBRACK:
                break
            