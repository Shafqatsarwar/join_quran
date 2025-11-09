export default function ChatWidget() {
  const chainlitUrl = process.env.NEXT_PUBLIC_CHAINLIT_URL || 'http://localhost:8001'

  const openChat = () => {
    window.open(chainlitUrl, 'chainlit_chat', 'width=900,height=800')
  }

  return (
    <div>
      <button onClick={openChat} className="btn">Open Chat (Chainlit UI)</button>
      <p style={{marginTop: 8}}>Chainlit runs separately — run it in the backend and open this button to view the chat UI.</p>
    </div>
  )
}
