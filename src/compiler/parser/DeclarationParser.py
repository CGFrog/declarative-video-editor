from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.StateVariable import Clip, StateVariable
from src.compiler.Effect import Effect
from src.compiler.parser.ParsingUtils import extract_duration, first_of_token,extract_function_parameters
class DeclarationParser():
    def __init__(self):
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.primitives: dict = {} # Holds num/string variables
        self.line_number : int = 1

    def parse_source(self, lines_of_tokens : list[list[Token]]):
        """
        Takes in a list of lists of tokens and returns the dict of states.
        """
        for tokens in lines_of_tokens:
            if len(tokens) == 0:
                continue
            
            token: TL = tokens[0].key
            match token:
                case TL.MEDIA:
                    if tokens[1].key != TL.IDENTIFIER: 
                        raise Exception(f"Invalid identifier after type declaration.")
                    self.state.update({tokens[1].value : self.__parse_media(tokens)})
                case TL.NUM | TL.STR:
                    self.__parse_primitive(tokens)
            self.line_number += 1

    def __parse_media(self, tokens : list[Token])->StateVariable:
        """
        When the parser detects a line dedicated to instantiating a media object, parse media determines:
        <ul>
            <li> Unions </li>
            <li> Trims </li>
            <li> Effects </li>
        </ul>

        returns StateVariable        
        """
        state_var = StateVariable()
        start_of_def: int = first_of_token(tokens, TL.DEFINITION)
        start_of_func: int = first_of_token(tokens,TL.FUNC_COMP)

        state_var.clips = self.__generate_clips(tokens[start_of_def:start_of_func:])
        state_var.effects = self.__generate_effects(tokens[start_of_func::])
        return state_var
    
    def __parse_primitive(self, tokens: list[Token]):
        """
        Parses primitive declarations like: 
        num opacity = 0.5"""
    
    def __generate_effects(self, tokens : list[Token])->list[Effect]:
        """
        Parses the effects of a line.
        """
        index = 0
        effects : list[Effect] = []
        while index < len(tokens):
            token = tokens[index]
            match token.key:
                case TL.EFFECT:
                    input_len: int = first_of_token(tokens[index::], TL.RPAREN)
                    if input_len < 0:
                        raise(Exception(f"Invalid function composition on {self.line_number}"))
                    effects.append(Effect(token.value, extract_function_parameters(tokens[index+1:index+ input_len:])))
                    index=input_len+ index
            index+=1
        effects.reverse()
        return effects
    
    def __generate_clips(self,tokens: list[Token])->list[Clip]:
        """
        Takes in tokens and returns lists of clips
        """
        index : int = 0
        clips: list[Clip] = []
        path: str = ""
    

        while index < len(tokens):
            token = tokens[index]
            match token.key:
                case TL.DEFINITION:
                    path = token.value
                case TL.LPAREN:
                    rparen: int = first_of_token(tokens[index+1::], TL.RPAREN)
                    duration: list[str] = extract_duration(tokens[index+1:index + rparen+1:])
                    clips.append(Clip(path, duration))
                    index = index + rparen
            index += 1
        return clips