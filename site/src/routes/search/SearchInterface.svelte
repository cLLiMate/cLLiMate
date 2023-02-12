<script>
  import pDebounce from "p-debounce";
  import { build_path } from "$lib/api.js";
  import Table from "$lib/Table.svelte";
  import { DoubleBounce } from "svelte-loading-spinners";
  import Plot from "$lib/Plot.svelte";

  let text = null;
  let data;
  let loaded = false;

  const phrases = [
    "reduce, reuse, recycle",
    "ocean acidification",
    "climate change",
    "sustainable living practices",
    "renewable energy revolution",
    "green transportation",
    "climate justice movement",
    "agriculture and food systems",
    "carbon capture and storage",
    "carbon sequestration",
    "ocean cleanup",
    "plastic pollution",
    "sustainable fashion"
  ];

  function randomPhrase() {
    return phrases[Math.floor(Math.random() * phrases.length)];
  }

  async function search(text, k = 100) {
    let url = build_path(import.meta.env.VITE_API_HOST, `articles/search?n_neighbors=${k}`, true);
    let resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });
    return await resp.json();
  }

  async function testReadyForSearch() {
    // We have to load the glove embedding on the backend, which takes 10-20 second on cold start.
    // We check on this and add a loading indicator until it's ready.
    await search("test query");

    // set loaded to true to enable the search bar
    loaded = true;
  }

  let debouncedSearch = pDebounce((text) => {
    search(text).then((res) => {
      data = res;
    });
  }, 500);
  $: text && debouncedSearch(text);

  $: options = {
    autoColumns: true,
    pagination: "local",
    paginationSize: 10,
    paginationCounter: "rows",
    autoColumnsDefinitions: [
      { field: "embedding", visible: false },
      { field: "headline", formatter: "link", formatterParams: { urlField: "url" } },
      { field: "url", visible: false },
      { field: "sentiment_score", formatter: (cell) => cell.getValue().toFixed(4) },
      { field: "distance", formatter: (cell) => cell.getValue().toFixed(4) }
    ]
  };
</script>

<div class="searchbar">
  <input
    type="text"
    bind:value={text}
    placeholder={`search: ${randomPhrase()}`}
    disabled={!loaded}
  />
  <button on:click={() => (text = loaded ? randomPhrase() : "loading search...")}
    >search random</button
  >
</div>

{#await testReadyForSearch()}
  <div class="loading">
    <DoubleBounce size="120" />
  </div>
{:then}
  {#if data}
    <div>
      <Table {data} {options} />
    </div>
    <div class="plots">
      <Plot
        {data}
        transform={(d) => [{ x: d.map((r) => r.distance), type: "histogram" }]}
        layout={{
          title: "Histogram of article distances (cosine)",
          xaxis: { title: "distances" },
          yaxis: { title: "Number of articles" }
        }}
      />
      <Plot
        {data}
        transform={(d) => [{ x: d.map((r) => r.sentiment_score), type: "histogram" }]}
        layout={{
          title: "Histogram of article sentiment scores",
          xaxis: { title: "sentiment scores" },
          yaxis: { title: "Number of articles" }
        }}
      />
    </div>
  {/if}
{/await}

<style>
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
  }
  .searchbar {
    display: flex;
  }
  .searchbar input {
    width: 100%;
    font-size: 1.5rem;
  }
  .searchbar button {
    font-size: 1.5rem;
    margin-left: 1rem;
  }
</style>
