export default function Counter({ initial }: { initial: number }) {
  const [count, setCount] = createSignal(initial ?? 0)
  const increment = () => setCount(v => v + 1)
  const decrement = () => setCount(v => v - 1)

  return (
    <div>
      {count()}
      <button class="inc" onClick={() => increment()}>
      +
      </button>
      <button class="dec" onClick={() => decrement()}>
      -
      </button>
    </div>
  )
}
