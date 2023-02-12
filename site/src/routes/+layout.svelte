<script>
  import "sakura.css/css/sakura.css";
  import { DateTime } from "luxon";

  export let data;
  let github_url = "https://github.com/cLLiMate/cLLiMate";
  $: site_status = data && data.site_status;
  $: api_status = data && data.api_status;
  $: build_time = site_status && DateTime.fromISO(site_status.build_time);
</script>

<main class="container">
  <nav class="box">
    <div>
      <a href="/">[ home ]</a>
      <a href="/search">[ search ]</a>
      <a href="/analysis">[ analysis ]</a>
      <a href="/api/v1/docs?client=true">[ openapi ]</a>
      <a href={github_url}>[ github ]</a>
    </div>
    {#if site_status && api_status}
      <div>
        <b>rev</b>:
        <a
          title={JSON.stringify({ site_status, api_status }, "", 2)}
          href="{github_url}/commit/{site_status.commit_sha}">v{site_status.version}</a
        >
        <b>build time</b>: {build_time.toLocaleString(DateTime.DATETIME_MED)}
      </div>
    {/if}
  </nav>
  <slot />
</main>

<style>
  a {
    text-decoration: none;
  }
  .box {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap-reverse;
  }
  main {
    margin-bottom: 1rem;
  }
</style>
