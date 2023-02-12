function build_path(base_url, path, client = false) {
  // if we request the content from the client directly, we need to account
  // for the nginx name from outside the docker netweork
  if (client) {
    base_url = base_url.replace("nginx", "localhost");
  }
  return `${base_url.replace(/\/$/, "")}/${path}`;
}

export async function get({ url, params, fetch }, base_url) {
  let client = url.searchParams.get("client") === "true";
  let redirect_url = build_path(base_url, params.slug, client);
  if (client) {
    console.log(`redirecting to ${redirect_url}`);
    return Response.redirect(redirect_url, 302);
  } else {
    console.log(`backend fetching ${redirect_url}`);
    return await fetch(redirect_url);
  }
}
