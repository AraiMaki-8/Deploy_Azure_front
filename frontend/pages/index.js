import { useState } from 'react';

export default function Home() {
  const [date, setDate] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      console.log("送信される日付:", date);  // 日付を確認
      const res = await fetch('http://localhost:5000/api/ask-date', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ date }),
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.status}`);  // ステータスコードの確認
      }

      const data = await res.json();
      setResponse(data);

    } catch (err) {
      console.error("エラーが発生しました", err);  // エラーをコンソールに出力
    }
  }

  //   const data = await res.json();
  //   setResponse(data);
  // };

  return (
    <div>
      <h1>今日は何の日？</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
        <button type="submit">送信</button>
      </form>
      {response && (
        <div>
          <h2>お答えします</h2>
          <p>ChatGPTの回答：{response.text}</p>
          {response.image_url && <img src={response.image_url} alt="関連画像" style={{maxWidth: '300px', marginTop: '10px'}} />}  {/* 画像を表示 */}
        </div>
      )}
    </div>
  );
}


