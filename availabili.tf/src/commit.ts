export default interface Commit {
  verified: boolean;
  html_url: string;
  sha: string;
  commit: {
    author: {
      name: string;
    };
    message: string;
  };
};
