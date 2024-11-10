import { AvailabilitfClient, CancelablePromise } from "@/client";
import { defineStore } from "pinia";

export const useClientStore = defineStore("client", () => {
  const client = new AvailabilitfClient({
    //BASE: import.meta.env.VITE_API_BASE_URL
  });

  const calls = new Map<string, Promise<any>>();

  function call<T>(
    key: string,
    apiCall: () => CancelablePromise<T>,
    thenOnce?: (result: T) => T
  ): Promise<T> {
    console.log("Fetching call " + key);
    if (!calls.has(key)) {
      const promise = apiCall();
      calls.set(key, promise);

      // remove from calls once completed
      promise.finally(() => calls.delete(key));

      // only execute this "then" once if the call was just freshly made
      if (thenOnce) {
        promise.then(thenOnce);
      }

      return promise;
    }
    return calls.get(key) as Promise<T>;
  }

  return {
    client,
    call,
    calls,
  }
});
