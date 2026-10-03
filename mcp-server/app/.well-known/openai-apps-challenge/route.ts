const TOKEN = "68cRBCq-gbYOMr_OwGPfR8T5D7qxkJvQILOnkLzjY7w";

export async function GET() {
  return new Response(TOKEN, {
    status: 200,
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
