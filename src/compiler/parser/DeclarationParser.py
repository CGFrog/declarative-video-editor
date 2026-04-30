from src.compiler.lexer.Token import Token, TokenLabel
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.VideoVariable import Clip, VideoVariable
from src.compiler.Effect import Effect
from src.compiler.parser.ParsingUtils import extract_duration, first_of_token, extract_function_parameters
from src.compiler.parser.Primitive import Primitive
from src.compiler.parser.ResolvedFunction import ResolvedFunction
from src.compiler.TextVariable import TextVariable

class DeclarationParser(): 
    def __init__(self): 
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.primitives: dict = {} # Holds all primitive variables i.e. num and str and acts as a look-up table when the compiler sees a variable used.
        self.functions: dict = {} # Holds all declared functions from end user and acts as a look-up table
        self.line_number : int = 1

    def parse_source(self, lines_of_tokens : list[list[Token]]):
        """
        Takes in a list of lists of tokens and returns the dict of states.
        """
        for tokens in lines_of_tokens:
            if len(tokens) == 0:
                continue
            declaratives: set[TL] = {TL.MEDIA, TL.STR, TL.CAPTION, TL.CAPTION, TL.NUM,TL.FUNC}
            
            if tokens[0].key in declaratives and tokens[1].key != TL.IDENTIFIER: 
                raise Exception(f"Invalid identifier after type declaration.")
            token: TL = tokens[0].key
            match token:
                case TL.MEDIA:
                    self.state.update({tokens[1].value : self.__parse_media(tokens)})
                case TL.STR: 
                    self.primitives.update({tokens[1].value : self.__parse_primitive_string(tokens)})
                case TL.CAPTION:
                    self.state.update({tokens[1].value: self.__parse_caption(tokens)})
                case TL.NUM:
                    self.primitives.update({tokens[1].value : self.__parse_primitive_number(tokens)})
                case TL.FUNC:
                    self.functions[tokens[1].value] = self.__parse_func_decl(tokens)
            self.line_number += 1


    def __parse_media(self, tokens : list[Token])->VideoVariable:
        """
        When the parser detects a line dedicated to instantiating a media object, parse media determines:
        <ul>
            <li> Unions </li>
            <li> Trims </li>
            <li> Effects </li>
        </ul>

        returns VideoVariable        
        """
        start_of_def: int = first_of_token(tokens, TL.DEFINITION)
        start_of_func: int = first_of_token(tokens,TL.FUNC_COMP)

        return VideoVariable(
            clips=self.__generate_clips(tokens[start_of_def:start_of_func:]),
            effects=self.__generate_effects(tokens[start_of_func::]),
            type=tokens[0].value
        )
    
    def __parse_primitive_number(self, tokens : list[Token]):
        eq_index = first_of_token(tokens, TL.ASSIGN)
        if eq_index >= len(tokens):
            raise Exception(f"Line {self.line_number}: missing '=' in number declaration.")
        value_token: Token = tokens[eq_index + 1]
        value:str = value_token.value
        return value
    
    def __parse_caption(self,tokens : list[Token])->TextVariable:
        name_token = tokens[1]
        caption = self.__parse_primitive_string(tokens)
        duration = None
        for token in tokens:
            if token.key == TL.NUMBER:
                duration = token.value
        if duration is None:
            raise Exception("Unspecified duration for caption.")
        return TextVariable(identifier=name_token.value, text=caption, duration=duration)

    def __parse_primitive_string(self, tokens : list[Token]):        
        eq_index = first_of_token(tokens, TL.ASSIGN)
        if eq_index >= len(tokens):
            raise Exception(f"Line {self.line_number}: missing '=' in primitive declaration.")
        
        curr_Idx = eq_index + 1
        curr_token = None
        try:
            curr_token = tokens[curr_Idx]
        except:
            raise Exception("No string after assignment, did you forget \"...\"?")
        return curr_token.value
        
    def __parse_func_decl(self, tokens : list[Token]) -> ResolvedFunction:
        """
        Parses through line containing keyword 'func', slices the tokens within the '()' 
        and returns identifier tokens. Body_tokens represent the entire pipeline right of the = sign.
        Then, validates the identifiers are within the parameters list, else raises exception. 
        Stores everything into a dict that gets saved into self.functions for later use.
        """
        
        left_paren = first_of_token(tokens, TL.LPAREN)
        right_paren = first_of_token(tokens, TL.RPAREN)

        params = []
        for token in tokens[left_paren+1:right_paren]:
            if token.key == TL.IDENTIFIER:
                params.append(token.value)
        
        eq_index = first_of_token(tokens, TL.ASSIGN)
        body_tokens = tokens[eq_index + 1:]

        for token in body_tokens:
            if token.key == TL.IDENTIFIER and token.value not in params:
                raise Exception(f"Line {self.line_number}: Undefined parameter '{token.value} in func body.")
        
        return ResolvedFunction(params, body_tokens)
        
    def resolve_params(self, raw_params: list[Primitive], primitives: dict) -> list:
        resolved = []

        for p in raw_params:
            match p.type:
                case "NUMBER":
                    resolved.append(p.value)
                case "STRING":
                    resolved.append(p.value)
                case "IDENTIFIER":
                    if p.value not in primitives:
                        raise Exception(f"Undefined variable: {p.value}")
                    resolved.append(primitives[p.value])
                case _:
                    raise Exception(f"Unknown parameter type {p.type}")
        
        return resolved
    
    
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
                    input_len: int = first_of_token(tokens[index:], TL.RPAREN)
                    if input_len < 0:
                        raise(Exception(f"Invalid function composition on {self.line_number}"))
                    
                    # Temp placeholder list 
                    raw_params = extract_function_parameters(tokens[index+1:index+input_len])

                    # Check parameters against self.primitives dict {}
                    resolved_params = self.resolve_params(raw_params, self.primitives)

                    # Bundle everything into an effect object from resolved_params
                    effects.append(Effect(token.value, resolved_params))
                    index=input_len+ index

                case TL.IDENTIFIER:
                    func_name = token.value
                    if func_name not in self.functions:
                        raise Exception(f"Line {self.line_number}: Unknown function '{func_name}'.")
                    func = self.functions[func_name]

                    right_paren = first_of_token(tokens[index:], TL.RPAREN)

                    # Extract the raw arguments between the ( and )
                    raw_args = extract_function_parameters(tokens[index+1:index+right_paren])
                    
                    # Resolve arguments against self.primitives in case any are variables e.g. f(Var1, 2, 3)
                    resolved_args = self.resolve_params(raw_args, self.primitives)
                    
                    # Validate argument count matches parameter count
                    if len(resolved_args) != len(func.params):
                        raise Exception(
                            f"Line {self.line_number}: '{func_name}' expects "
                            f"{len(func.params)} args, got {len(resolved_args)}."
                        )
                    # Create a temporary local dict pairing each parameter name with its argument value
                    local_vars = dict(zip(func.params, resolved_args))
                    
                    # Evaluate the function body using local_vars and collect the resulting effects
                    expanded_effects = self.__generate_effects_with_localVars(func.body, local_vars)
                    effects.extend(expanded_effects)
                    index += right_paren

            index+=1
        effects.reverse()
        return effects

    # Walks through tokens and builds a list of Effect objects 
    def __generate_effects_with_localVars(self, tokens: list[Token], local_vars: dict) -> list[Effect]:
        """
        Evaluates a declared function's body tokens using the local variable DICT created in __generate_effects.
        Called when a user defined function like f(1,2,3) is found in a pipe chain.
        It resolves parameters against local_vars which maps parameter names to their 
        passed in argument values. (e.g. local_vars = {"a": 1, "b": 2, "c": 3})
        Returns a list of Effect objects with the arguments substituted in.
        """        
        index = 0
        effects: list[Effect] = []
        while index < len(tokens):
            token = tokens[index]
            match token.key:
                case TL.EFFECT:
                    input_len = first_of_token(tokens[index:], TL.RPAREN)
                    if input_len < 0:
                        raise Exception(f"Invalid function body on line {self.line_number}")
                    raw_params = extract_function_parameters(tokens[index+1:index+input_len])
                    resolved_params = self.resolve_params(raw_params, local_vars)
                    effects.append(Effect(token.value, resolved_params))
                    index += input_len
            index += 1
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