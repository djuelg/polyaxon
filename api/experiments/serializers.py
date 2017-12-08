# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus,
)


class ExperimentJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    job = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJobStatus
        exclude = ('id',)

    def get_job(self, obj):
        return obj.job.uuid.hex


class ExperimentJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJob
        exclude = ('id',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex


class ExperimentStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentStatus
        exclude = ('id',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex


class ExperimentSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    cluster = fields.SerializerMethodField()
    spec = fields.SerializerMethodField()
    project = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = ('uuid', 'user', 'name', 'created_at', 'updated_at',
                  'last_status', 'started_at', 'finished_at', 'is_clone',
                  'cluster', 'project', 'spec',)

    def get_user(self, obj):
        return obj.user.username

    def get_cluster(self, obj):
        return obj.cluster.uuid.hex

    def get_spec(self, obj):
        return obj.spec.uuid.hex if obj.spec else None

    def get_project(self, obj):
        return obj.project.uuid.hex


class ExperimentDetailSerializer(ExperimentSerializer):
    jobs = ExperimentJobSerializer(many=True)

    class Meta(ExperimentSerializer.Meta):
        fields = ExperimentSerializer.Meta.fields + (
            'description', 'config', 'original_experiment', 'jobs',)


class ExperimentCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()
    
    class Meta:
        model = Experiment
        fields = (
            'cluster', 'project', 'user', 'name', 'description',
            'spec', 'config', 'original_experiment')
        extra_kwargs = {
            'cluster': {'write_only': True},
            'project': {'write_only': True},
            'spec': {'write_only': True}
        }

    def get_user(self, obj):
        return obj.user.username
