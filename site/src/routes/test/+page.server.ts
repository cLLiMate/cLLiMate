import type { LoadEvent } from "@sveltejs/kit";

export async function load({ fetch }: LoadEvent) {
  let resp = await fetch(["/api/v1/data/vis", "all-v4.json"].join("/"));
  return {
    agreement: await resp.json()
  };
}
