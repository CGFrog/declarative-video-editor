from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.StateVariable import Clip, StateVariable
from src.compiler.Effect import Effect

class DeclarationParser():
    def __init__(self):
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.line_number : int = 1

    def parse_source(self, lines_of_tokens : list[list[Token]]):
        for tokens in lines_of_tokens:
            if len(tokens) == 0:
                continue
            
            token: TL = tokens[0].key
            match token:
                case TL.MEDIA:
                    if tokens[1].key != TL.IDENTIFIER: 
                        raise Exception(f"Invalid identifier after type declaration.")
                    self.state.update({tokens[1].value : self.__parse_media(tokens)})
            self.line_number += 1
        return self.state

    def __parse_media(self, tokens : list[Token]):
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
        start_of_def: int = self.__first_of_token(tokens, TL.DEFINITION)
        start_of_func: int = self.__first_of_token(tokens,TL.FUNC_COMP)

        state_var.clips = self.__generate_clips(tokens[start_of_def:start_of_func:])
        state_var.effects = self.__generate_effects(tokens[start_of_func::])
        return state_var
    
    def __first_of_token(self, tokens: list[Token], token: TL)-> int:
        for (i, t) in enumerate(tokens, start=0):
            if t.key == token:
                return i
        return len(tokens)
    
    def __generate_effects(self, tokens : list[Token])->list[Effect]:
        index = 0
        effects : list[Effect] = []
        while index < len(tokens):
            token = tokens[index]
            match token.key:
                case TL.EFFECT:
                    input_len: int = self.__first_of_token(tokens[index::], TL.RPAREN)
                    if input_len < 0:
                        raise(Exception(f"Invalid function composition on {self.line_number}"))
                    effects.append(Effect(token.value, self.__extract_function_parameters(tokens[index+1:index+ input_len:])))
                    index=input_len+ index
            index+=1
        return effects
    
    def __extract_function_parameters(self, tokens: list[Token]) ->list:
        params = []
        for token in tokens:
            if token.key == TL.NUMBER:
                params.append(token.value)
        return params
    
    def __generate_clips(self,tokens: list[Token])->list[Clip]:
        index : int = 0
        clips: list[Clip] = []
        path: str = ""
    

        while index < len(tokens):
            token = tokens[index]
            match token.key:
                case TL.DEFINITION:
                    path = token.value
                case TL.LPAREN:
                    rparen: int = self.__first_of_token(tokens[index+1::], TL.RPAREN)
                    duration: list[str] = self.__extract_duration(tokens[index+1:index + rparen+1:]).split(',')
                    clips.append(Clip(path, duration))
                    index = index + rparen
            index += 1
        return clips
    
    def __extract_duration(self, tokens: list[Token])-> str:
        return "".join(t.value for t in tokens)
    