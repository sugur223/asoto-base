export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">
          asotobase
        </h1>
        <p className="text-center text-lg mb-4">
          あそびと仕事をつなぐプラットフォーム
        </p>
        <div className="flex gap-4 justify-center mt-8">
          <a
            href="/login"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            ログイン
          </a>
          <a
            href="/register"
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
          >
            新規登録
          </a>
        </div>
      </div>
    </main>
  )
}
