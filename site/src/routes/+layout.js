async function fetch_site_status(fetch) {
  const resp = await fetch("/status");
  return await resp.json();
}

async function fetch_api_status(fetch) {
  const resp = await fetch("/api/v1/status");
  return await resp.json();
}

export async function load({ fetch }) {
  // get site and api status at the same time
  const [site_status, api_status] = await Promise.all([
    fetch_site_status(fetch),
    fetch_api_status(fetch)
  ]);
  return { site_status, api_status };
}
