from __future__ import absolute_import, unicode_literals

from app import app


@app.route("/")
def zen():
    return """
    <ul>
        <li><strong>It is cached:</strong> {cached}</li>
        <li><strong>It is not cached:</strong> {not_cached}</li>
    </ul>
    """.format(
        cached='TESTING THINGS',
        not_cached='TESTING THINGS'
    )