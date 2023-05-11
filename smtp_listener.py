#####################################
######## Quick SMTP Listener ########
###### Dan Duran - GetCyber.Me ######
#####################################

import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Envelope

class CustomSMTPServer:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print(f"Received message from: {envelope.mail_from}")
        print(f"To: {envelope.rcpt_tos}")
        print("Message:")
        print(envelope.content.decode('utf-8'))
        print("=" * 50)
        return '250 Message accepted for delivery'

    async def handle_CLOSE(self, server, session):
        pass

async def run_smtp_server():
    handler = CustomSMTPServer()
    controller = Controller(handler, hostname='[YOUR IP]', port=25)
    controller.start()

async def shutdown(server):
    server.close()
    await server.wait_closed()

if __name__ == "__main__":
    print("Starting SMTP server...")
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(run_smtp_server())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown(server))
        loop.close()
