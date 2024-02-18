import { Component, ErrorInfo, ReactNode } from 'react';
import { YMInitializer } from 'react-yandex-metrika';
import { ErrorComponent } from '../ErrorComponent/ErrorComponent';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      hasError: false,
    };
  }

  public static getDerivedStateFromError(_: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  render() {
    const { hasError } = this.state;
    const { children } = this.props;

    return (
      <>
        {hasError ? <ErrorComponent isWrongPage /> : children}
        <YMInitializer accounts={[94470504]} version="2" />
      </>
    );
  }
}

export default ErrorBoundary;
