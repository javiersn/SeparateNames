from sys import stdin, argv
import pandas as pd   # TODO: replace pandas for simple file reading, and remove import
from enum import Enum
from typing import List, Dict, Optional, Mapping
from unidecode import unidecode


class Order(Enum):
    SN = -1
    UK = 0
    NS = 1


class TokenType(Enum):
    NAME = -2
    LIKE_NAME = -1
    AMBIGUOUS = 0
    LIKE_SURNAME = 1
    SURNAME = 2


name_ds = pd.read_csv('./Data/Names_SSA.csv', usecols=[0, 1, 2], index_col=0)   # TODO: find localized name datasets
name_ds['scaled'] = name_ds['Frequency'] / name_ds['Frequency'].max()
surname_ds = pd.read_csv('./Data/Surnames_USCENSUS.csv', usecols=[0, 1], index_col=0)
surname_ds['scaled'] = surname_ds['Frequency'] / surname_ds['Frequency'].max()
prefixes_df = pd.read_csv('./Data/Prefixes.csv', usecols=[0])
prefix_ds = list(prefixes_df['Prefix'])


class NameToken:
    def __init__(self, s: str, is_prefix: bool = False, name_prob: float = 0, surname_prob: float = 0,
                 tktype: int = None):
        self.value: str = s
        self.is_prefix = is_prefix
        self.name_prob = name_prob
        self.surname_prob = surname_prob
        self.tktype = tktype
        self.deleted: bool = False

    def qualify(self) -> TokenType:
        """
        Evaluates the token's type using the global dictionaries for names, surnames and prefixes, and stores
        the resulting TokenType Enum value (LIKE_NAME | LIKE_SURNAME | AMBIGUOUS) into the tktype property.
        :return:  the assigned TokenType.
        """
        if unidecode(self.value.upper()) in prefix_ds:
            self.is_prefix = True
        if unidecode(self.value.upper()) in name_ds.index:
            self.name_prob = name_ds.loc[unidecode(self.value.upper()), 'scaled']
        if unidecode(self.value.upper()) in surname_ds.index:
            self.surname_prob = surname_ds.loc[unidecode(self.value.upper()), 'scaled']
        if self.name_prob > self.surname_prob:
            self.tktype = TokenType.LIKE_NAME
        elif self.surname_prob > self.name_prob:
            self.tktype = TokenType.LIKE_SURNAME
        else:
            self.tktype = TokenType.AMBIGUOUS
        return self.tktype

    def prepend(self, s: str) -> str:
        """
        Prepends a specified string to the value property of the NameToken object, and stores the modified string as
        the new value property.
        :param s: the string to prepend to the value.
        :return:  the modified string.
        """
        self.value = s + ' ' + self.value
        return self.value

    def print(self):
        """
        Prints the NameToken object's property values.
        """
        print('Actual Value:   {}'.format(self.value))
        print('Is Prefix:      {}'.format(self.is_prefix))
        print('Is Name (P):    {}'.format(self.name_prob))
        print('Is Surname (P): {}'.format(self.surname_prob))
        print('Token Type:     {}'.format(self.tktype))


class NameSplitter:
    def __init__(self, full_name: str = None, order: Order = None):
        self.full_name: str = full_name
        self.order: Order = order
        self.name: str = None
        self.first_surname: str = None
        self.second_surname: str = None
        self.tokens: List[NameToken] = []
        self.order_guess_map: Dict = {   # Invoke as _map_order[first_token_type, last_token_type], and it returns
            TokenType.LIKE_NAME: {        # guessed type for the first token.
                TokenType.LIKE_NAME: Order.UK,
                TokenType.AMBIGUOUS: Order.NS,
                TokenType.LIKE_SURNAME: Order.NS
            },
            TokenType.AMBIGUOUS: {
                TokenType.LIKE_NAME: Order.SN,
                TokenType.AMBIGUOUS: Order.UK,
                TokenType.LIKE_SURNAME: Order.NS
            },
            TokenType.LIKE_SURNAME: {
                TokenType.LIKE_NAME: Order.SN,
                TokenType.AMBIGUOUS: Order.SN,
                TokenType.LIKE_SURNAME: Order.UK
            }
        }

    def get_tokens(self) -> List[NameToken]:
        """
        Splits the given full name into tokens, one for each word found, and then proceeds to identify prefix tokens
        (i.e. Von, Mac, Do, Du, etc.) and group them into their corresponding token. And stores the split name into
        the tokens property.
        :return:  a list of NameToken objects corresponding to the split full name.
        """
        tokens: List[NameToken] = list(map(lambda s: NameToken(s), self.full_name.split()))
        length = len(tokens)
        for t in tokens:
            t.qualify()
        for i, t in enumerate(tokens):
            if t.is_prefix and i < length-1:
                tokens[i+1].prepend(t.value)
                t.deleted = True
        self.tokens = [t for t in tokens if not t.deleted]
        return self.tokens

    def guess_order(self) -> Optional[Order]:
        """
        If an order wasn't previously assigned, deduces the most likely form or order of the full name (i.e.: 'name
        first' or 'surname first') and stores the enfered order into the order property.
        :return: the infered order as a value of the Order Enum (UK for unknown, NS for name first, and SN for sur-
        name first).
        """
        if self.order is None or self.order == Order.UK:
            length = len(self.tokens)
            if length < 2:
                print("Token list [{}] is empty or too short. Initialized full name and use get_tokens() first.".
                      format(", ".join([x.value for x in self.tokens])))
                return None
            else:
                self.order = self.order_guess_map[self.tokens[0].tktype][self.tokens[length - 1].tktype]
                if self.order == Order.UK:
                    if (self.tokens[0].name_prob > self.tokens[length-1].name_prob) or \
                            (self.tokens[0].surname_prob < self.tokens[length-1].surname_prob):
                        self.order = Order.NS
                    elif (self.tokens[0].name_prob < self.tokens[length-1].name_prob) or \
                            (self.tokens[0].surname_prob > self.tokens[length-1].surname_prob):
                        self.order = Order.SN
                    else:
                        self.order = Order.NS

    def adjust_tokens(self) -> None:
        """
        Assigns a definitive TokenType to each token, taking into consideration the position of each token and the
        order of the tokens (name first or surname first). Stores the final TokenType into the tktype property of
        each token.
        :return:  None
        """
        if self.order is None or self.order == Order.UK:
            self.guess_order()
        length = len(self.tokens)
        if length < 2:
            print("Token list [{}] is empty or too short. Ensure full name was initialized and use get_tokens() first.".
                  format(", ".join([x.value for x in self.tokens])))
            return None
        if self.order == Order.NS:
            self.tokens[0].tktype = TokenType.NAME
            self.tokens[length-1].tktype = TokenType.SURNAME
            if length > 2:
                self.tokens[length-2].tktype = TokenType.NAME \
                    if self.tokens[length-2].name_prob > self.tokens[length-2].surname_prob * 2 \
                    else TokenType.SURNAME
                if length > 3:
                    self.tokens[1].tktype = TokenType.SURNAME \
                        if self.tokens[1].surname_prob > self.tokens[1].name_prob * 2 \
                        else TokenType.NAME
        elif self.order == Order.SN:
            self.tokens[0].tktype = TokenType.SURNAME
            self.tokens[length-1].tktype = TokenType.NAME
            if length > 2:
                self.tokens[1].tktype = TokenType.NAME \
                    if self.tokens[1].name_prob > self.tokens[1].surname_prob * 2 \
                    else TokenType.SURNAME
                if length > 3:
                    self.tokens[length-2].tktype = TokenType.SURNAME \
                        if self.tokens[length-2].surname_prob > self.tokens[length-2].name_prob * 2 \
                        else TokenType.NAME
        if length > 4:
            for i in range(2, length-2):
                self.tokens[i].tktype = TokenType.NAME \
                    if self.tokens[i].name_prob > self.tokens[i].surname_prob * 3/2 \
                    else TokenType.SURNAME
        return None

    def split_name(self) -> Optional[Mapping[str, str]]:
        """
        Once the tokens have been assigned definitive TokenType, and an order has been infered or given, groups
        the tokens into first name, first surname, and second surname. Stores the grouped tokens as strings in-
        to the first_name, first_surname and second_surname properties respectively.
        :return:  A dictionary of strings, detailing the name, first_surname and last_surname values.  Or
        None if the script fails.
        """
        types: List[TokenType] = [t.tktype for t in self.tokens]
        length: int = len(self.tokens)
        if length < 2:
            print("Token list [{}] is empty or too short. Ensure full name was initialized and use get_tokens() first.".
                  format(", ".join([x.value for x in self.tokens])))
            return None
        if self.order is None or self.order == Order.UK:
            print("Order has not been set. guess_order() must be called before splitting")
            return None
        if TokenType.LIKE_NAME in types or TokenType.LIKE_SURNAME in types or TokenType.AMBIGUOUS in types:
            print("Some tokens are still unqualified. adjust_tokens() must be called before splitting")
            return None
        elif self.order == Order.NS:
            switch = types.index(TokenType.SURNAME)
            self.name = " ".join([t.value for t in self.tokens[0:switch]])
            switch2 = int((length - switch) / 2 + switch) if length - switch > 1 else length + 1
            self.first_surname = " ".join([t.value for t in self.tokens[switch:switch2]])
            self.second_surname = " ".join([t.value for t in self.tokens[switch2:length]])
        elif self.order == Order.SN:
            switch = types.index(TokenType.NAME)
            self.name = " ".join([t.value for t in self.tokens[switch:length]])
            switch2 = int(switch / 2) if switch > 1 else switch
            self.first_surname = " ".join([t.value for t in self.tokens[0:switch2]])
            self.second_surname = " ".join([t.value for t in self.tokens[switch2:switch]])
        return {'name': self.name, 'first_surname': self.first_surname, 'last_surname': self.second_surname}


def split_name(fullname: str, order: int = None):
    """
    Splits a full name (latin style) string into name, first surname and second surname by creating a
    NameSplitter object and invoking the necessary methods to achieve the split.
    :param fullname:  the full name string to split into parts.
    :param order:  optionally, the order in which the full name is stated (-1 for surname first, and
    1 for name first).
    :return:  a dictionary of strings, detailing the name, first_surname and last_surname values. Or
    None if the script fails.
    """
    ns = NameSplitter(fullname, Order(order) if order is not None else None)
    ns.get_tokens()
    ns.guess_order()
    ns.adjust_tokens()
    return ns.split_name()


if __name__ == '__main__':
    names = []
    options = ''
    force_order = None
    if len(argv) > 1:
        names += [i.strip() for i in argv[1:] if i[0] != '-']
        options += ''.join([i for i in argv[1:] if i[0] == '-']).replace('-', '').strip()
    if len(options) > 0:
        if options == 'on':
            force_order = Order.NS
        elif options == 'os':
            force_order = Order.SN
        else:
            raise ValueError("Unknown option(s) specified: -{}".format(options))
    if not stdin.isatty():
        names += stdin.readlines()
    if len(names) > 0:
        for n in names:
            if len(n) > 0:
                print(split_name(n, force_order))   # TODO: add other formats for output: CSV or Lists
    else:
        print("""
    Usage:
        $ python ./SeparateNames.py [-on|-os] ['Name 1'] ['Name 2'] ...
        
    If -on or -os is specified, all names will be considered in 'name first' or 'surname first' forms
    respectively. If none of these options is specified, the order will be guessed for each name in--
    dividually.
    
    Also accepts a list of names through stdin, in the form
        $ cat names.txt | python ./SeparateNames.py [-on|-os] ['Name 1'] ['Name 2'] ...
    
    IMPORTANT NOTICE: the script uses name and surname dictionaries in order to identify and separate
    name. These dictionaries were obtained from publicly available datasets provided by the U.S. So--
    cial Security (SSA) and the U.S. and the U.S. Census Bureau (USCENSUS).""")
