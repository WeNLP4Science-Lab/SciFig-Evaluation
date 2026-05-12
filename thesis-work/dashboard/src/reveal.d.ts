declare module 'reveal.js' {
  interface RevealOptions {
    hash?: boolean
    slideNumber?: boolean | string
    progress?: boolean
    controls?: boolean
    controlsTutorial?: boolean
    transition?: string
    transitionSpeed?: string
    backgroundTransition?: string
    center?: boolean
    width?: number
    height?: number
    margin?: number
    minScale?: number
    maxScale?: number
    [key: string]: unknown
  }

  class Reveal {
    constructor(element: HTMLElement, options?: RevealOptions)
    initialize(): Promise<void>
    destroy(): void
    slide(h: number, v?: number, f?: number): void
    getState(): unknown
    configure(options: RevealOptions): void
  }

  export default Reveal
}

declare module 'reveal.js/dist/reveal.css' {
  const content: string
  export default content
}
