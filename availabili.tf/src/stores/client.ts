import { AvailabilitfClient, CancelablePromise } from "@/client";
import { defineStore } from "pinia";

export const useClientStore = defineStore("client", () => {
  const client = new AvailabilitfClient({
    //BASE: import.meta.env.VITE_API_BASE_URL
  });

  const calls = new Map<string, Promise<any>>();

  type CachedValue<T> = {
    value: T,
    timestamp: number,
  };

  const cached = new Map<string, any>();

  function callCached<T>(
    key: string,
    apiCall: () => CancelablePromise<T>,
    maxLifetime: number = 2000,
    thenOnce?: (result: T) => T,
    catchOnce?: (error: any) => any,
    finallyOnce?: () => void,
  ): Promise<T> {
    if (cached.has(key)) {
      const cachedValue = cached.get(key) as CachedValue<T>;
      if (Date.now() - cachedValue.timestamp < maxLifetime) {
        return Promise.resolve(cachedValue.value);
      }
    }

    // cache miss
    let promise = call(key, apiCall, thenOnce, catchOnce, finallyOnce);
    promise.then((result) => {
      cached.set(key, {
        value: result,
        timestamp: Date.now(),
      });
    });
    return promise;
  }

  function call<T>(
    key: string,
    apiCall: () => CancelablePromise<T>,
    thenOnce?: (result: T) => T,
    catchOnce?: (error: any) => any,
    finallyOnce?: () => void,
  ): Promise<T> {
    console.log("Fetching call " + key);
    if (!calls.has(key)) {
      console.log("Making new call " + key);
      const promise = apiCall();
      calls.set(key, promise);

      // remove from calls once completed
      promise.finally(() => {
        console.log("Call " + key + " completed");
        calls.delete(key);
      });

      // only execute this "then" once if the call was just freshly made
      if (thenOnce) {
        promise.then(thenOnce);
      }

      if (catchOnce) {
        promise.catch(catchOnce);
      }

      if (finallyOnce) {
        promise.finally(finallyOnce);
      }

      return promise;
    } else {
      console.log("Returning concurrent call " + key);
    }
    return calls.get(key) as Promise<T>;
  }

  return {
    client,
    call,
    callCached,
    calls,
  }
});
