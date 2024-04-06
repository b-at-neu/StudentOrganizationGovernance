from django.db import models
from copy import deepcopy

class DuplicatingModel(models.Model):
    """
        Deep copies a model including all foreign key references (M2M is not copied)
    """
    def deep_copy(self):

        """
        Returns all related objects for a model recursively
        """
        def get_related_objects(model, related_objects):

            related_objects_list = []

            # Iterate through all the fields in the parent object looking for related fields            
            for field in model._meta.get_fields():
                if field.one_to_many:
                    objects = getattr(model, field.name)
                    if objects:
                        related_objects_list += list(objects.all())
                    
                    # Recursive call
                    for object in objects.all():
                        related_objects = get_related_objects(object, related_objects)

            if related_objects_list:
                related_objects.append({
                    "model": model,
                    "related_objects": related_objects_list
                })

            return related_objects


        related_objects = get_related_objects(self, [])

        # Duplicate the parent object
        self.pk = None
        self.save()

        # Loop over each parent model and each object related to it
        for model in reversed(related_objects):
            for related_object in model["related_objects"]:
                # Iterate through the fields in the related object to find the one that relates to the parent model
                for related_object_field in related_object._meta.fields:
                    if related_object_field.related_model == model["model"].__class__:
                        # If the related_model on this field matches the parent object's class, perform the
                        # copy of the child object and set this field to the parent object, creating the
                        # new child -> parent relationship.
                        old_related_object = deepcopy(related_object)

                        related_object.pk = None
                        setattr(related_object, related_object_field.name, model["model"])
                        related_object.save()

                        # Replace the old references
                        for i in related_objects:
                            if i["model"] == old_related_object:
                                i["model"] = related_object

        return self
    
    class Meta:
        abstract = True