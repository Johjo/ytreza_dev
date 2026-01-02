from dataclasses import dataclass
from typing import Any, NewType

from expression import Nothing, Option, Some


def test_read_nothing_when_no_mail() -> None:
    truc = Truc()
    mail = read_next_mail(truc)
    assert mail == Nothing


MailTitle = NewType("MailTitle", str )
MailBody = NewType("MailBody", str )

@dataclass(frozen=True, eq=True)
class Mail:
    title: MailTitle
    body: MailBody


@dataclass(frozen=True, eq=True)
class MailBuilder:
    title: MailTitle=MailTitle("the title")
    body: MailBody=MailBody("the body")

    def build(self) -> Mail:
        return Mail(self.title, self.body)


class Truc:
    def __init__(self) -> None:
        self.mail = Nothing

    def feed(self, mail: MailBuilder) -> None:
        self.mail = Some(mail.build())

    def read_next_mail(self) -> Option[Mail]:
        return self.mail





def a_mail() -> MailBuilder:
    return MailBuilder()


def test_read_mail() -> None:
    truc = Truc()
    expected = a_mail()
    truc.feed(expected)
    mail = read_next_mail(truc)
    assert mail == Some(expected.build())


def read_next_mail(truc: Truc) -> Option[Mail]:
    return truc.read_next_mail()
