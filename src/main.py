from core import add_message, check_and_add_system_message, connect_db, get_messages, initialize_db, send_message
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
            reply = send_message(get_messages(conn), tools)

            if reply.tool_calls:

                result = tool_call(reply)
                tool_name = reply.tool_calls[0].function.name
                add_message("IA", f"[a demandé l'outil {tool_name}]", conn)
                add_message("tool", result, conn)

                final_reply = send_message(get_messages(conn), tools).content
                add_message("IA", final_reply, conn)
                print("IA : ", final_reply)

            else:
                add_message("IA", reply.content, conn)
                print("IA : ", reply.content)
        except Exception as e:
            print("Erreur : ", e)
            continue
finally:
    conn.close()
    print("Connexion à la base de données fermée.")
