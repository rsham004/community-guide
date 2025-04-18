function MetricCard({ title, value, subtitle, icon, color = 'primary' }) {
  const colorClasses = {
    primary: 'text-primary',
    secondary: 'text-secondary',
    accent1: 'text-accent-1',
    accent2: 'text-accent-2'
  };

  return (
    <div className="card flex flex-col">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
        {icon && <span className="text-gray-400">{icon}</span>}
      </div>
      <p className={`text-3xl font-bold ${colorClasses[color] || 'text-primary'}`}>
        {value}
      </p>
      {subtitle && <p className="text-sm text-text-secondary mt-1">{subtitle}</p>}
    </div>
  );
}

export default MetricCard;
