<script>
  import ThreeDPlot from "./ThreeDPlot.svelte";
  import TestPlot from "./TestPlot.svelte";
  export let data;
  console.log(data.agreement.GroupOne);
</script>

# Analysis for Climate News Articles

### Number of Articles

Key Takeaway: Although news sources decrease in their reporting of climate change, academics and researchers are ever more interested, evidenced by the sharp increase in Nature articles.

<TestPlot agreement={data.agreement.GroupZero} />

### Sentiment Analysis over time

Even though positive and negative sentiment remain constant, the strength of neutral articles increases, representing a shift in mindset about the issues that surround climate change.

<TestPlot agreement={data.agreement.GroupOne} />

### Sentiment types of Articles over time

Although the vast majority of news articles are neutral, there is a clear shift toward negativity surrounding the topic, as the number negative articles increases and positive trends downward.

<TestPlot agreement={data.agreement.GroupTwo} />

### Clustering for Articles

Using LDA and K-means clustering, we found 6 groups that roughly represent articles in the climate news dataset, and represented this in the 3d feature plot below.

Experiment with the interactivity!

<ThreeDPlot agreement={data.agreement.umapClimate} />
