import type Commit from "@/commit";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCommitsStore = defineStore("commits", () => {
  const commits = ref<Commit[]>([]);
  const commitsMap = ref<{ [id: string]: Commit }>({ });

  function fetchCommits() {
    const user = "HumanoidSandvichDispenser";
    const repo = "availabili.tf";

    if (commits.value.length == 0) {
      fetch(`https://api.github.com/repos/${user}/${repo}/commits`)
        .then((response) => response.json())
        .then((response: Commit[]) => {
          commits.value = response;
          response.forEach((commit) => {
            commitsMap.value[commit.sha] = commit;
          });
        });
    }
  }

  return {
    commits,
    commitsMap,
    fetchCommits,
  };
});
