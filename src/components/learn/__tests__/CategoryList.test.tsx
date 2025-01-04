import { render, screen, fireEvent } from '@/lib/test-utils'
import { CategoryList } from '../CategoryList'

const mockCategories = [
  {
    id: '1',
    name: 'Test Category',
    description: 'Test Description',
    icon: 'brain',
    created_at: new Date().toISOString()
  }
]

describe('CategoryList', () => {
  it('renders categories correctly', () => {
    render(
      <CategoryList
        categories={mockCategories}
        selectedCategoryId={null}
        onCategorySelect={() => {}}
        courseCount={() => 0}
      />
    )

    expect(screen.getByText('Test Category')).toBeInTheDocument()
  })

  it('calls onCategorySelect when clicking a category', () => {
    const mockOnSelect = jest.fn()
    render(
      <CategoryList
        categories={mockCategories}
        selectedCategoryId={null}
        onCategorySelect={mockOnSelect}
        courseCount={() => 0}
      />
    )

    fireEvent.click(screen.getByText('Test Category'))
    expect(mockOnSelect).toHaveBeenCalledWith('1')
  })
})