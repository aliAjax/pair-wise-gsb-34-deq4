import { useEffect, useRef } from "react";

// 弹窗等组件挂载时执行一次异步加载，避免依赖数组导致重复请求
export function useAsyncOnce(effect: () => void, deps: ReadonlyArray<unknown> = []) {
  const firedRef = useRef(false);
  useEffect(() => {
    if (firedRef.current) return;
    firedRef.current = true;
    effect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
