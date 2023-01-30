import { cleanup, fireEvent, render } from 'solid-testing-library'
import { afterEach, describe, expect, it } from 'vitest'
import Counter from '../src/components/Counter'

describe('Counter', () => {
  afterEach(cleanup)

  it('should render', () => {
    const { getByText } = render(() => <Counter initial={10}/>)
    expect(getByText('10')).toBeDefined()
  })

  it('should be interactive', () => {
    const { getByText } = render(() => <Counter initial={0}/>)
    expect(getByText('0')).toBeDefined()

    fireEvent.click(getByText('+') as Element)

    expect(getByText('1')).toBeDefined()
  })
})
