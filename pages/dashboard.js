import { useEffect } from 'react';

export default function Dashboard() {
  useEffect(() => {
    // Логика загрузки данных дашборда
  }, []);

  return (
    <div>
      <h1>Дашборд</h1>
      <button>
        <svg className="lucide-plus" width="24" height="24">
          <path d="M12 5v14M5 12h14" />
        </svg>
        Создать проект
      </button>
    </div>
  );
}