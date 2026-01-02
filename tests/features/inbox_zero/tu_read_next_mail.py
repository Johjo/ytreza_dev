from dataclasses import dataclass
from typing import NewType

from expression import Nothing, Option, Some


def test_read_nothing_when_no_mail() -> None:
    email_reader = EmailReader()

    inbox_reader = InboxReader(email_reader)
    mail = inbox_reader.next_item()
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


class EmailReader:
    def __init__(self) -> None:
        self.mail = Nothing

    def feed(self, mail: MailBuilder) -> None:
        self.mail = Some(mail.build())

    def read_next_mail(self) -> Option[Mail]:
        return self.mail





def a_mail() -> MailBuilder:
    return MailBuilder()


def test_read_mail() -> None:
    email_reader = EmailReader()
    expected = a_mail()
    email_reader.feed(expected)
    inbox_reader = InboxReader(email_reader)
    mail = inbox_reader.next_item()
    assert mail == Some(expected.build())


class InboxReader:
    def __init__(self, email_reader: EmailReader) -> None:
        self._email_reader = email_reader

    def next_item(self) -> Option[Mail]:
        return self._email_reader.read_next_mail()


