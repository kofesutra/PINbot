async def cbqa(call, bot):
    query = call.id
    await bot.answer_callback_query(callback_query_id=query)
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
