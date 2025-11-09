/** Next.js config for simple static and API routing. Use env NEXT_PUBLIC_BACKEND_URL to point to the API. */
module.exports = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_BACKEND_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
  }
}
