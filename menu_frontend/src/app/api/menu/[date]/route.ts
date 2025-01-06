import { NextResponse } from 'next/server';

export const GET = async (
  request: Request,
  { params }: { params: { date: string } }
) => {
  try {
    const { date } = params;
    const { searchParams } = new URL(request.url);
    const lang = searchParams.get('lang') || 'en';  // 기본값을 영어로 설정
    
    const response = await fetch(`http://localhost:8080/api/menu/${date}?lang=${lang}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch menu');
    }
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching menu:', error);
    return NextResponse.json(
      { error: 'Failed to fetch menu', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
}
