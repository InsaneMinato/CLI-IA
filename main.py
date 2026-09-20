import os


try:
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            print("À la prochaine !")
            break

        #best_doc = find_best_document(user_input, doc_embeddings)

        messages.append({"role": "user", "content": user_input})
        save_message("user", user_input)

        #messages_with_context = messages + [{"role": "system", "content": "Voici un document qui peut t'aider : " + docs[best_doc]}]

        try:
            response = client.chat.complete(
                model="mistral-small-latest",
                messages= messages,
                tools=tools
            )

            reply = response.choices[0].message
            reply_content = reply.content

            if reply.tool_calls:
                tool_name = reply.tool_calls[0].function.name
                arguments = reply.tool_calls[0].function.arguments
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                print("Le modèle veut appeler :", tool_name)

                if tool_name == "get_current_time":
                    result = get_current_time()

                if tool_name == "get_file_content":
                    file_path = arguments.get("file_path")
                    result = get_file_content(file_path)

                if tool_name == "modify_file_content":
                    file_path = arguments.get("file_path")
                    old_content = arguments.get("old_content")
                    new_content = arguments.get("new_content")

                    result = modify_file_content(file_path, old_content, new_content)


                messages.append(reply)
                save_message("assistant", f"[a demandé l'outil {tool_name}]")
                messages.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": result,
                    "tool_call_id": reply.tool_calls[0].id
                })
                response2 = client.chat.complete(
                    model="mistral-small-latest",
                    messages=messages,
                    tools=tools
                )
                final_reply = response2.choices[0].message.content
                messages.append({"role": "assistant", "content": final_reply})
                print("IA : ", final_reply)



            else:
                messages.append({"role": "assistant", "content": reply_content})
                save_message("assistant", reply_content)
                print("IA : ", reply_content)
        except Exception as e:
            print("Erreur, réessaie :", e)
            continue
finally:
    if conn:
        conn.close()
