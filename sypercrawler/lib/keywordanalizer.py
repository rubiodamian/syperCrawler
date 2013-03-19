from __future__ import division
import  re
import unicodedata
from collections import Counter


class KeywordAnalizer(object):
    _slugify_strip_re = re.compile(r'[^\w\s-]')
    _slugify_hyphenate_re = re.compile(r'[-\s]+')

    def slugify(self, value, separator=' '):
        if not isinstance(value, unicode):
            value = unicode(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(self._slugify_strip_re.sub('', value).strip().lower())
        return str(self._slugify_hyphenate_re.sub(separator, value))

    def keywordDensity(self, nkr, tkn):
        ''' Where Nkr is how many times you repeated a specific keyword and Tkn the total words in the analyzed text.
        Returns the round percent of this formula'''
        return round((nkr / tkn) * 100)

    def checkForKeywordStuffing(self, string):
        text = self.slugify(string)
        words = list(x for x in text.split(" ") if x not in self.stopWords())
        wordsCount = len(words)
        if(wordsCount >= 10):
            wordsCounter = Counter(words)
            return self.keywordDensity(wordsCounter.most_common(1)[0][1], wordsCount) > 3
        else:
            return False

    def stopWords(self):
        return ['a', 'aca', 'ahi', 'ajena', 'ajenas', 'ajeno', 'ajenos', 'al', 'algo', 'algun',
        'alguna', 'algunas', 'alguno', 'algunos', 'alla', 'alli', 'alli', 'ambos', 'ampleamos',
        'ante', 'antes', 'aquel', 'aquella', 'aquellas', 'aquello', 'aquellos', 'aqui', 'aqui',
        'arriba', 'asi', 'atras', 'aun', 'aunque', 'bajo', 'bastante', 'bien', 'cabe',
        'cada', 'casi', 'cierta', 'ciertas', 'cierto', 'ciertos', 'como', 'como', 'con',
        'conmigo', 'conseguimos', 'conseguir', 'consigo', 'consigue', 'consiguen',
        'consigues', 'contigo', 'contra', 'cual', 'cuales', 'cualquier', 'cualquiera',
        'cualquieras', 'cuan', 'cuan', 'cuando', 'cuanta', 'cuanta', 'cuantas', 'cuantas',
        'cuanto', 'cuanto', 'cuantos', 'cuantos', 'de', 'dejar', 'del', 'demas', 'demas',
        'demasiada', 'demasiadas', 'demasiado', 'demasiados', 'dentro', 'desde', 'donde',
        'dos', 'el', 'el', 'ella', 'ellas', 'ello', 'ellos', 'empleais', 'emplean', 'emplear',
        'empleas', 'empleo', 'en', 'encima', 'entonces', 'entre', 'era', 'eramos', 'eran', 'eras',
        'eres', 'es', 'esa', 'esas', 'ese', 'eso', 'esos', 'esta', 'estaba', 'estado', 'estais',
        'estamos', 'estan', 'estar', 'estas', 'este', 'esto', 'estos', 'estoy', 'etc', 'fin',
        'fue', 'fueron', 'fui', 'fuimos', 'gueno', 'ha', 'hace', 'haceis', 'hacemos', 'hacen',
        'hacer', 'haces', 'hacia', 'hago', 'hasta', 'incluso', 'intenta', 'intentais',
        'intentamos', 'intentan', 'intentar', 'intentas', 'intento', 'ir', 'jamas', 'junto',
        'juntos', 'la', 'largo', 'las', 'lo', 'los', 'mas', 'mas', 'me', 'menos', 'mi', 'mia',
        'mia', 'mias', 'mientras', 'mio', 'mio', 'mios', 'mis', 'misma', 'mismas', 'mismo',
        'mismos', 'modo', 'mucha', 'muchas', 'muchisima', 'muchisimas', 'muchisimo', 'muchisimos',
        'mucho', 'muchos', 'muy', 'nada', 'ni', 'ningun', 'ninguna', 'ningunas', 'ninguno',
        'ningunos', 'no', 'nos', 'nosotras', 'nosotros', 'nuestra', 'nuestras', 'nuestro',
        'nuestros', 'nunca', 'os', 'otra', 'otras', 'otro', 'otros', 'para', 'parecer', 'pero',
        'poca', 'pocas', 'poco', 'pocos', 'podeis', 'podemos', 'poder', 'podria',
        'podriais', 'podriamos', 'podrian', 'podrias', 'por', 'por', 'que', 'porque',
        'primero', 'primero', 'desde', 'puede', 'pueden', 'puedo', 'pues', 'que', 'que',
        'querer', 'quien', 'quien', 'quienes', 'quienesquiera', 'quienquiera', 'quiza',
        'quizas', 'sabe', 'sabeis', 'sabemos', 'saben', 'saber', 'sabes', 'se', 'segun',
        'ser', 'si', 'si', 'siempre', 'siendo', 'sin', 'sin', 'sino', 'so', 'sobre', 'sois',
        'solamente', 'solo', 'somos', 'soy', 'sr', 'sra', 'sres', 'sta', 'su', 'sus', 'suya',
        'suyas', 'suyo', 'suyos', 'tal', 'tales', 'tambien', 'tambien', 'tampoco',
        'tan', 'tanta', 'tantas', 'tanto', 'tantos', 'te', 'teneis', 'tenemos', 'tener',
        'tengo', 'ti', 'tiempo', 'tiene', 'tienen', 'toda', 'todas', 'todo', 'todos',
        'tomar', 'trabaja', 'trabajais', 'trabajamos', 'trabajan', 'trabajar', 'trabajas',
        'trabajo', 'tras', 'tu', 'tu', 'tus', 'tuya', 'tuyo', 'tuyos', 'ultimo', 'un',
        'una', 'unas', 'uno', 'unos', 'usa', 'usais', 'usamos', 'usan', 'usar', 'usas',
        'uso', 'usted', 'ustedes', 'va', 'vais', 'valor', 'vamos', 'van', 'varias',
        'varios', 'vaya', 'verdad', 'verdadera', 'vosotras', 'vosotros', 'voy', 'vuestra',
        'vuestras', 'vuestro', 'vuestros', 'y', 'ya', 'yo', 'a', 'about', 'above',
        'above', 'across', 'after', 'afterwards', 'again',
        'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
        'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
        'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as',
        'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before',
        'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill',
        'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt',
        'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
        'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every',
        'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find',
        'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from',
        'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence',
        'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
        'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed',
        'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly',
        'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine',
        'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely',
        'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
        'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other',
        'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps',
        'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several',
        'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow',
        'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system',
        'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence',
        'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these',
        'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through',
        'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards',
        'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via',
        'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever',
        'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon',
        'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever',
        'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would',
        'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '']
