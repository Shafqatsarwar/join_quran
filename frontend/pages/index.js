import Head from 'next/head'
import useSWR from 'swr'
import Header from '../components/Header'
import ChatWidget from '../components/ChatWidget'

const fetcher = (url) => fetch(url).then(r => r.json())

export default function Home() {
  const { data } = useSWR(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/site`, fetcher)

  return (
    <div>
      <Head>
        <title>Join Quran - Demo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <Header />

      <main className="container">
        <section className="hero">
          <h1>{data?.title || 'Join Quran (Demo)'}</h1>
          <p>{data?.tagline || 'Learn Quran with structured classes, teachers and community.'}</p>
          <div className="cta">
            <a className="btn" href="#classes">View Classes</a>
            <a className="btn outline" href="#contact">Contact</a>
          </div>
        </section>

        <section id="classes" className="section">
          <h2>Featured Classes</h2>
          <ul>
            {(data?.classes || []).map((c) => (
              <li key={c.id}>{c.title} — {c.level}</li>
            ))}
          </ul>
        </section>

        <section id="chat" className="section">
          <h2>Chat with the assistant</h2>
          <p>You can open the Chainlit chat UI (runs separately) or use the embedded widget to open the chat UI in a new tab.</p>
          <ChatWidget />
        </section>

        <section id="contact" className="section">
          <h2>Contact</h2>
          <p>Use the contact form on the real site. This demo is static and for local testing only.</p>
        </section>
      </main>

      <footer className="site-footer">
        <small>Demo created for local testing. Not the official site.</small>
      </footer>
    </div>
  )
}
