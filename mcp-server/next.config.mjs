/** Keep OpenAI plugin domain verification a strict plain-text response.
 * The public challenge is a token, not an HTML/JSON document.
 */
const challengeHeaders = [
  { key: "Content-Type", value: "text/plain; charset=utf-8" },
  { key: "Cache-Control", value: "no-store" },
];

export default {
  async headers() {
    return [
      { source: "/.well-known/openai-apps-challenge", headers: challengeHeaders },
      { source: "/openai-apps-challenge", headers: challengeHeaders },
    ];
  },
};
