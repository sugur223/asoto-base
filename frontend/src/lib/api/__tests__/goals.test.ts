import { fetchGoals, createGoal, updateGoal, deleteGoal } from '../goals';
import { apiClient } from '../client';

jest.mock('../client');

describe('Goals API', () => {
  const mockApiClient = apiClient as jest.Mocked<typeof apiClient>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('fetchGoals', () => {
    it('fetches goals successfully', async () => {
      const mockGoals = [
        {
          id: '1',
          user_id: 'user1',
          title: 'Test Goal',
          category: 'activity',
          status: 'active',
          progress: 0,
          created_at: '2025-01-01T00:00:00Z',
          updated_at: '2025-01-01T00:00:00Z',
        },
      ];

      mockApiClient.get.mockResolvedValue({ data: mockGoals });

      const result = await fetchGoals();

      expect(mockApiClient.get).toHaveBeenCalledWith('/goals');
      expect(result).toEqual(mockGoals);
    });

    it('handles fetch error', async () => {
      mockApiClient.get.mockRejectedValue(new Error('Network error'));

      await expect(fetchGoals()).rejects.toThrow('Network error');
    });
  });

  describe('createGoal', () => {
    it('creates goal successfully', async () => {
      const newGoal = {
        title: 'New Goal',
        description: 'Description',
        category: 'activity' as const,
      };

      const mockResponse = {
        id: '1',
        ...newGoal,
        user_id: 'user1',
        status: 'active',
        progress: 0,
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z',
      };

      mockApiClient.post.mockResolvedValue({ data: mockResponse });

      const result = await createGoal(newGoal);

      expect(mockApiClient.post).toHaveBeenCalledWith('/goals', newGoal);
      expect(result).toEqual(mockResponse);
    });
  });

  describe('updateGoal', () => {
    it('updates goal successfully', async () => {
      const goalId = '1';
      const updateData = { status: 'completed' as const };

      const mockResponse = {
        id: goalId,
        title: 'Test Goal',
        category: 'activity',
        user_id: 'user1',
        status: 'completed',
        progress: 100,
        created_at: '2025-01-01T00:00:00Z',
        updated_at: '2025-01-01T00:00:00Z',
      };

      mockApiClient.patch.mockResolvedValue({ data: mockResponse });

      const result = await updateGoal(goalId, updateData);

      expect(mockApiClient.patch).toHaveBeenCalledWith(`/goals/${goalId}`, updateData);
      expect(result.status).toBe('completed');
    });
  });

  describe('deleteGoal', () => {
    it('deletes goal successfully', async () => {
      const goalId = '1';

      mockApiClient.delete.mockResolvedValue({ data: null });

      await deleteGoal(goalId);

      expect(mockApiClient.delete).toHaveBeenCalledWith(`/goals/${goalId}`);
    });
  });
});
