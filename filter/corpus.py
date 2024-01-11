from email import message_from_file
from html import unescape
from os import listdir
from os.path import isfile, join
from re import compile, findall, sub
from filter.utils import read_classification_from_file

class Corpus:
    def __init__(self, corpus_dir):
        self.tags = compile("<.*?>")
        self.alphabet = compile(r"([a-zA-Z0-9\-]*)")
        self.corpus_dir = corpus_dir


    def get_emails(self):
        emails = [f for f in listdir(self.corpus_dir) if isfile(join(self.corpus_dir, f))]
        for email in emails:
            if email.startswith("!"):
                continue
                    
            message = self.__parse_email(email)   
            yield message


    def get_email_words(self, email):
        vocab = list()
        message = email.get("msg", "")

        for line in message.splitlines():
            for word in line.strip().split():
                for cleaned in findall(self.alphabet, word.strip()):
                    if cleaned != '': # Used regex rto ged rid of some nasty stuff driving match rates low
                        vocab.append(cleaned.lower())
        return vocab


    def write_predicted_tags(self, tags):
        with open(join(self.corpus_dir, "!prediction.txt"), "wt", encoding="utf-8") as p:
            for tag in tags.items():
                p.write(tag[0] + " " + tag[1] + "\n")


    def __parse_email(self, email_fn):
        parsed_mail = dict()

        # Read email from file
        with open(join(self.corpus_dir, email_fn), "rt", encoding='utf-8') as f:
            message = message_from_file(f)
            
            for part in message.walk():
                part_payload = part.get_payload(decode=True)

                if part.get_content_type() == 'text/plain':
                    # No aditional parsing required
                    parsed_mail["msg"] = parsed_mail.get("msg", "") + unescape(str(part_payload).replace("\\n", "\n"))

                elif part.get_content_type() == 'text/html':
                    detagged = sub(self.tags, " ", str(part_payload))
                    parsed_mail["msg"] = parsed_mail.get("msg", "") + unescape(str(detagged).replace("\\n", "\n"))
                else:
                    # Other than text/plain ant text/html shouldn't occur. But if so, treat it as text/plain
                    parsed_mail["msg"] = parsed_mail.get("msg", "") + unescape(str(part_payload).replace("\\n", "\n"))
            
            # Some of these params went unused
            parsed_mail["from"] = message["From"]
            parsed_mail["raw_msg"] = parsed_mail.get("raw_msg", "") + str(part_payload)
            parsed_mail["content_type"] = message.get_content_type()
            parsed_mail["filename"] = email_fn

        return parsed_mail
        