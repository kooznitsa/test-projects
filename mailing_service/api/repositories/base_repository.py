from sqlmodel.ext.asyncio.session import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _upsert_value(self, result, model, model_create):
        """Insert or update a value.

        It is used to create a value in the database if it does not already exist,
        else it is used to update the existing one.

        Args:
          result:
            The model data.
          model:
            Model (table schema) instance.
          model_create:
            ModelCreate (data schema) instance.

        Returns:
          The upserted model.
        """
        model_from_orm = model.from_orm(model_create)

        # if the entity does not exist, create it
        if result is None:
            result = model_from_orm

        # sync the data
        for k, v in model_from_orm.dict(exclude_unset=True).items():
            setattr(result, k, v)

        return result
