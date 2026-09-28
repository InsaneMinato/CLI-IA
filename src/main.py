from core import add_message, check_and_add_system_message, connect_db, get_messages, initialize_db, send_message, delete_all_messages
from services import get_tools, tool_call

conn = connect_db()

try:
    initialize_db(conn)
    check_and_add_system_message(conn)

    tools = get_tools()

    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            print("À la prochaine !")
            break

        add_message("user", user_input, conn)

        try:
            messages = get_messages(conn)
            reply = send_message(messages, tools)

            if reply.tool_calls:
                result = tool_call(reply)
                assistant_message = reply.model_dump(exclude_none=True)
                messages.extend([
                    assistant_message,
                    {"role": "tool", "content": result},
                ])

                final_reply = send_message(messages, tools).content
                add_message("IA", final_reply, conn)
                print("IA : ", final_reply)

            else:
                add_message("IA", reply.content, conn)
                print("IA : ", reply.content)
        except Exception as e:
            print("Erreur : ", e)
            continue
finally:
    delete_all_messages(conn)
    conn.close()
    print("Connexion à la base de données fermée.")
