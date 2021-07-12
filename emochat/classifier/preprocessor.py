import spacy


class Preprocessor:
    ALL_STOPWORDS = ['zehntes', 'dein', 'derselben', 'habe', 'das', 'zwar', 'wahr', 'wie', 'kannst', 'drittes', 'aber',
                     'konnte', 'hätten', 'will', 'andern', 'oder', 'währenddessen', 'seine', 'hin', 'wollten', 'daß',
                     'fünften', 'sagt', 'geschweige', 'mancher', 'darum', 'vielen', 'solang', 'jedermann', 'demgemäss',
                     'jeder', 'jede', 'haben', 'viele', 'vom', 'besser', 'jahr', 'können', 'jemand', 'währenddem',
                     'siebentes', 'dementsprechend', 'könnt', 'allein', 'musst', 'darüber', 'achte', 'vergangene',
                     'zugleich', 'durfte', 'hoch', 'mehr', 'außerdem', 'dürfen', 'aus', 'ihr', 'solcher', 'keinem',
                     'vergangenen', 'weiteren', 'nichts', 'früher', 'nach', 'seiner', 'erster', 'erstes', 'trotzdem',
                     'weitere', 'kleine', 'demselben', 'so', 'darunter', 'es', 'meinem', 'besonders', 'solchen',
                     'zehnter', 'grossen', 'meinen', 'welche', 'mögen', 'schlecht', 'wegen', 'wenig', 'unsere', 'zeit',
                     'damals', 'dermassen', 'natürlich', 'neunter', 'genug', 'erste', 'gemocht', 'neuen', 'denen',
                     'kommt', 'kann', 'kein', 'neuntes', 'warum', 'musste', 'gern', 'wirst', 'alle', 'machte', 'dazu',
                     'ging', 'gutes', 'machen', 'ach', 'diejenige', 'ganze', 'dieses', 'mein', 'na', 'neunten',
                     'dritter', 'bereits', 'sechster', 'allen', 'ihnen', 'dazwischen', 'einiger', 'über', 'en', 'mich',
                     'von', 'werden', 'kaum', 'ihrem', 'dagegen', 'nie', 'ausserdem', 'neue', 'ob', 'sein', 'tat',
                     'anderen', 'deine', 'danach', 'groß', 'jedoch', 'wurden', 'seinem', 'zweiten', 'durch', 'achter',
                     'einen', 'deswegen', 'damit', 'rechte', 'möchte', 'daran', 'keiner', 'magst', 'auch', 'vielem',
                     'derjenigen', 'anders', 'kurz', 'dort', 'sondern', 'um', 'ins', 'neun', 'dasein', 'meines',
                     'großer', 'wird', 'tag', 'einmaleins', 'sei', 'zehnten', 'tage', 'ihren', 'als', 'davor', 'acht',
                     'große', 'eigener', 'geworden', 'siebente', 'denselben', 'allgemeinen', 'dritten', 'meine', 'wann',
                     'gar', 'vielleicht', 'gut', 'hat', 'demgegenüber', 'mag', 'eines', 'weniger', 'zunächst', 'statt',
                     'anderem', 'könnte', 'dafür', 'beide', 'keinen', 'jeden', 'infolgedessen', 'niemandem', 'leicht',
                     'jenes', 'gerade', 'grosser', 'irgend', 'jahre', 'dieser', 'wo', 'jene', 'willst', 'ehrlich',
                     'allerdings', 'jedermanns', 'waren', 'seid', 'deiner', 'ab', 'jedem', 'sechs', 'vier', 'hätte',
                     'während', 'bisher', 'ganzes', 'manche', 'kommen', 'muß', 'diesem', 'dieselben', 'demzufolge',
                     'ganzer', 'niemanden', 'bist', 'rechter', 'denn', 'tagen', 'wessen', 'immer', 'dahin', 'habt',
                     'siebtes', 'im', 'dieselbe', 'niemand', 'sehr', 'desselben', 'offen', 'solches', 'bei', 'wenn',
                     'elf', 'diejenigen', 'einige', 'sollen', 'wollte', 'weniges', 'dasselbe', 'wollen', 'siebter',
                     'du', 'seines', 'des', 'dies', 'weil', 'seien', 'besten', 'und', 'mochten', 'vierte', 'eigenen',
                     'á', 'jahren', 'mit', 'erst', 'zuerst', 'euch', 'dahinter', 'zu', 'auf', 'an', 'seit', 'wir',
                     'bin', 'gibt', 'sah', 'man', 'darfst', 'dabei', 'ebenso', 'ihn', 'wieder', 'sich', 'andere',
                     'werde', 'würden', 'jenem', 'hatte', 'sechsten', 'solchem', 'sagte', 'derjenige', 'gross',
                     'großes', 'seinen', 'einmal', 'richtig', 'ersten', 'etwa', 'unserer', 'weiter', 'den', 'war',
                     'worden', 'vierten', 'zusammen', 'geht', 'doch', 'manchen', 'gemacht', 'hast', 'gehen', 'satt',
                     'oben', 'dadurch', 'macht', 'ohne', 'wer', 'leider', 'her', 'wenigstens', 'hinter', 'je', 'vor',
                     'für', 'alles', 'eine', 'drin', 'demgemäß', 'sechste', 'zwischen', 'was', 'diese', 'sind', 'wohl',
                     'zur', 'dem', 'ja', 'nun', 'viel', 'dessen', 'rund', 'meiner', 'ganzen', 'nachdem', 'noch', 'soll',
                     'tel', 'wirklich', 'dank', 'sie', 'uns', 'welchen', 'deinem', 'wenige', 'fünfte', 'deshalb',
                     'weiteres', 'dritte', 'drei', 'gedurft', 'siebenten', 'gekannt', 'am', 'manchem', 'der', 'deren',
                     'hatten', 'kleinen', 'kleines', 'beispiel', 'kleiner', 'jemandem', 'lange', 'er', 'wen', 'mir',
                     'eigene', 'sieben', 'gewollt', 'also', 'großen', 'bald', 'endlich', 'möglich', 'gekonnt', 'in',
                     'mittel', 'solche', 'bekannt', 'später', 'grosses', 'nur', 'neunte', 'ein', 'übrigens', 'zwei',
                     'keine', 'muss', 'einiges', 'schon', 'eigen', 'welchem', 'nahm', 'heißt', 'ganz', 'los', 'nein',
                     'eigenes', 'manches', 'oft', 'heute', 'siebenter', 'zweiter', 'darauf', 'jenen', 'allem', 'dass',
                     'sechstes', 'durften', 'siebten', 'wäre', 'daher', 'gemusst', 'derselbe', 'wart', 'mussten',
                     'jemanden', 'teil', 'einander', 'selbst', 'würde', 'einigen', 'jener', 'recht', 'viertes',
                     'zwanzig', 'guter', 'mögt', 'uhr', 'a', 'die', 'zurück', 'rechtes', 'aller', 'dich', 'fünf',
                     'jetzt', 'lieber', 'dermaßen', 'sollten', 'weit', 'wollt', 'diesen', 'grosse', 'daselbst', 'ihrer',
                     'unter', 'etwas', 'gab', 'ist', 'morgen', 'sowie', 'überhaupt', 'sollte', 'achten', 'dann',
                     'einer', 'dürft', 'zehnte', 'gute', 'neben', 'gesagt', 'beim', 'welches', 'unser', 'außer',
                     'gegenüber', 'seitdem', 'werdet', 'müsst', 'zweite', 'fünftes', 'ausser', 'bis', 'da', 'daraus',
                     'indem', 'ich', 'müssen', 'fünfter', 'heisst', 'gehabt', 'einem', 'siebte', 'mochte', 'gleich',
                     'darf', 'ihm', 'ende', 'ihres', 'achtes', 'sonst', 'davon', 'daneben', 'wem', 'ag', 'zehn',
                     'wurde', 'zweites', 'entweder', 'nicht', 'eben', 'hier', 'ihre', 'gewesen', 'gegen', 'konnten',
                     'vierter', 'welcher', 'darin', 'beiden', 'durchaus', 'lang', 'rechten', 'zum', 'kam', 'dir', 'tun']

    def __init__(self):
        self.sp = spacy.load('de_core_news_sm')

    def preprocess_data(self, text):
        processed_text = text

        # Removal of unnecessary white spaces | Lowercasing
        processed_text = processed_text.strip().lower()
        return self.get_tokens(processed_text)

    def get_tokens(self, text):
        text_tokens = self.sp.tokenizer(text)
        string_tokens = []
        for word in text_tokens:
            if not (str(word) in self.ALL_STOPWORDS or str(word) in ('', ' ')):
                string_tokens.append(str(word))
        return string_tokens



