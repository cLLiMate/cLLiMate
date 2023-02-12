import { get } from "$lib/api.js";

export async function GET({ url, params, fetch }) {
  return await get({ url, params, fetch }, `${import.meta.env.VITE_STATIC_HOST}/data`);
}
